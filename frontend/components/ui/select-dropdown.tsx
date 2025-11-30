'use client'

import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from '@/components/ui/select'

interface SelectDropdownProps<T extends { [key: string]: any }> {
  items: T[]
  value: string | undefined
  onChange: (value: string) => void
  valueKey?: keyof T
  labelKey?: keyof T
  disabledKey?: keyof T
  className?: string
}

export function SelectDropdown<T extends Record<string, any>>({
  items,
  value,
  onChange,
  valueKey = 'value',
  labelKey = 'label',
  disabledKey = 'disabled',
  className,
}: SelectDropdownProps<T>) {
  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger className={className}>
        <SelectValue />
      </SelectTrigger>

      <SelectContent>
        {items.map((item) => (
          <SelectItem
            key={String(item[valueKey])}
            value={String(item[valueKey])}
            disabled={Boolean(item[disabledKey])}
          >
            {item[labelKey]}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}
