import { NextRequest, NextResponse } from 'next/server'
import * as XLSX from 'xlsx'
import Papa from 'papaparse'
import type { LogData } from '@/features/drilling/types/drilling.types'

// Field mappings for header recognition
const fieldMappings: Record<string, string[]> = {
  depth: ['depth', 'md', 'measured depth', 'depth_md', 'depth (ft)', 'depth_ft'],
  dt: ['dt', 'sonic', 'dtco', 'compressional slowness', 'dt_us/ft'],
  gr: ['gr', 'gamma ray', 'gr_api', 'gamma'],
  sh: ['sh', 'shale', 'shale volume', 'vsh'],
  anh: ['anh', 'anhydrite', 'anhydrite volume', 'anh_vol'],
  ls: ['ls', 'limestone', 'limestone volume', 'ls_vol'],
  coal: ['coal', 'coal volume', 'coal_vol'],
  salt: ['salt', 'salt volume', 'salt_vol'],
  dol: ['dol', 'dolomite', 'dolomite volume', 'dol_vol'],
}

export interface ParseFileResponse {
  data: LogData[]
  filename: string
  fileType: string
}

/**
 * Parses a value to number, handling strings with % and trimming
 */
function parseNumber(value: unknown, context: string): number {
  if (typeof value === 'number') return value
  if (typeof value === 'string') {
    const cleaned = value.replace(/^%/, '').trim()
    const parsed = parseFloat(cleaned)
    if (isNaN(parsed)) {
      throw new Error(`${context}: Invalid number "${value}"`)
    }
    return parsed
  }
  throw new Error(`${context}: Expected number, got ${typeof value}`)
}

/**
 * Parses JSON data from Excel (array of arrays) into LogData
 */
function parseJsonData(data: unknown[][]): LogData[] {
  if (data.length < 2) {
    throw new Error('File must contain at least a header row and one data row')
  }

  const headers = (data[0] as (string | number | null | undefined)[]).map((h) =>
    h?.toString().toLowerCase().replace(/^%/, '').trim()
  )
  const rows = data.slice(1)

  const columnIndices: Record<string, number> = {}

  // Find column indices using field mappings
  Object.keys(fieldMappings).forEach((field) => {
    for (const alias of fieldMappings[field]) {
      const index = headers.indexOf(alias.toLowerCase())
      if (index !== -1) {
        columnIndices[field] = index
        break
      }
    }
  })

  // At minimum, depth is required
  if (columnIndices.depth === undefined) {
    throw new Error(
      `File must contain a depth column. Supported names: ${fieldMappings.depth.join(', ')}`
    )
  }

  // Filter out rows with invalid or missing depth
  const validRows = rows.filter((row) => {
    const val = row[columnIndices.depth]
    return val !== undefined && val !== null && val !== ''
  })

  if (validRows.length === 0) {
    throw new Error('No valid data rows found with depth values')
  }

  // Convert rows to LogData objects
  const logData: LogData[] = validRows.map((row, index) => {
    try {
      const depth = parseNumber(row[columnIndices.depth], `Row ${index + 2}, depth`)

      const logData: LogData = { depth }

      // Parse optional columns
      ;['dt', 'gr', 'sh', 'anh', 'ls', 'coal', 'salt', 'dol'].forEach((col) => {
        if (columnIndices[col] !== undefined) {
          const value = row[columnIndices[col]]
          if (value !== null && value !== undefined && value !== '') {
            const parsed = parseNumber(value, `Row ${index + 2}, ${col}`)
            // Convert rock composition from decimal to percentage
            if (['sh', 'anh', 'ls', 'coal', 'salt', 'dol'].includes(col)) {
              logData[col as keyof LogData] = parsed * 100
            } else {
              logData[col as keyof LogData] = parsed
            }
          }
        }
      })

      return logData
    } catch (error) {
      throw new Error(
        `Row ${index + 2}: ${error instanceof Error ? error.message : 'Invalid data'}`
      )
    }
  })

  return logData
}

/**
 * Parses object data from CSV into LogData
 */
function parseObjectData(data: Record<string, unknown>[]): LogData[] {
  if (data.length === 0) {
    throw new Error('No data found in CSV file')
  }

  const headers = Object.keys(data[0])
  const lowerHeaders = headers.map((h) => h.toLowerCase().replace(/^%/, '').trim())

  const columnIndices: Record<string, number> = {}

  // Find column indices using field mappings
  Object.keys(fieldMappings).forEach((field) => {
    for (const alias of fieldMappings[field]) {
      const index = lowerHeaders.indexOf(alias.toLowerCase())
      if (index !== -1) {
        columnIndices[field] = index
        break
      }
    }
  })

  // At minimum, depth is required
  if (columnIndices.depth === undefined) {
    throw new Error(
      `File must contain a depth column. Supported names: ${fieldMappings.depth.join(', ')}`
    )
  }

  // Filter out rows with invalid or missing depth
  const validData = data.filter((row) => {
    const val = row[headers[columnIndices.depth]]
    return val !== undefined && val !== null && val !== ''
  })

  if (validData.length === 0) {
    throw new Error('No valid data rows found with depth values')
  }

  // Convert to LogData objects
  const logData: LogData[] = validData.map((row, index) => {
    try {
      // Normalize row keys to lowercase and strip %
      const normalizedRow: Record<string, unknown> = {}
      Object.keys(row).forEach((key) => {
        normalizedRow[key.toLowerCase().trim().replace(/^%/, '')] = row[key]
      })

      // Find depth value
      let depthValue: unknown
      for (const alias of fieldMappings.depth) {
        if (normalizedRow[alias.toLowerCase()] !== undefined) {
          depthValue = normalizedRow[alias.toLowerCase()]
          break
        }
      }
      if (depthValue === undefined) {
        throw new Error(`Missing depth column. Supported names: ${fieldMappings.depth.join(', ')}`)
      }
      const depth = parseNumber(depthValue, `Row ${index + 2}, depth`)

      const logData: LogData = { depth }

      // Parse optional columns
      ;['dt', 'gr', 'sh', 'anh', 'ls', 'coal', 'salt', 'dol'].forEach((col) => {
        let value: unknown
        for (const alias of fieldMappings[col]) {
          if (normalizedRow[alias.toLowerCase()] !== undefined) {
            value = normalizedRow[alias.toLowerCase()]
            break
          }
        }
        if (value !== null && value !== undefined && value !== '') {
          const parsed = parseNumber(value, `Row ${index + 2}, ${col}`)
          // Convert rock composition from decimal to percentage
          if (['sh', 'anh', 'ls', 'coal', 'salt', 'dol'].includes(col)) {
            logData[col as keyof LogData] = parsed * 100
          } else {
            logData[col as keyof LogData] = parsed
          }
        }
      })

      return logData
    } catch (error) {
      throw new Error(
        `Row ${index + 2}: ${error instanceof Error ? error.message : 'Invalid data'}`
      )
    }
  })

  return logData
}

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File

    if (!file) {
      return NextResponse.json({ error: 'No file provided' }, { status: 400 })
    }

    const fileExtension = file.name.split('.').pop()?.toLowerCase()

    if (!fileExtension || !['xlsx', 'xls', 'csv'].includes(fileExtension)) {
      return NextResponse.json(
        {
          error: 'Unsupported file format. Please upload Excel (.xlsx, .xls) or CSV (.csv) files.',
        },
        { status: 400 }
      )
    }

    const buffer = await file.arrayBuffer()
    let jsonData: any[] = []

    if (fileExtension === 'xlsx' || fileExtension === 'xls') {
      // Parse Excel file
      const workbook = XLSX.read(buffer, { type: 'buffer' })
      const sheetName = workbook.SheetNames[0]
      const worksheet = workbook.Sheets[sheetName]

      // Convert to JSON
      jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 })

      const parsedData = parseJsonData(jsonData as unknown[][])

      return Promise.resolve(
        NextResponse.json({
          data: parsedData,
          filename: file.name,
          fileType: fileExtension,
        } as ParseFileResponse)
      )
    } else if (fileExtension === 'csv') {
      // Parse CSV file
      const csvText = new TextDecoder().decode(buffer)

      return new Promise<Response>((resolve) => {
        Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          complete: (results) => {
            try {
              if (results.errors.length > 0) {
                resolve(
                  NextResponse.json(
                    {
                      error: `CSV parsing error: ${results.errors[0].message}`,
                    },
                    { status: 400 }
                  )
                )
                return
              }

              const parsedData = parseObjectData(results.data as Record<string, unknown>[])

              resolve(
                NextResponse.json({
                  data: parsedData,
                  filename: file.name,
                  fileType: fileExtension,
                } as ParseFileResponse)
              )
            } catch (error) {
              resolve(
                NextResponse.json(
                  {
                    error: error instanceof Error ? error.message : 'Failed to parse CSV data',
                  },
                  { status: 400 }
                )
              )
            }
          },
          error: (error: any) => {
            resolve(
              NextResponse.json(
                {
                  error: `CSV parsing error: ${error.message}`,
                },
                { status: 400 }
              )
            )
          },
        })
      })
    }

    return NextResponse.json({ error: 'Unsupported file type' }, { status: 400 })
  } catch (error) {
    console.error('File parsing error:', error)
    return NextResponse.json(
      {
        error: 'Failed to parse file',
      },
      { status: 500 }
    )
  }
}
