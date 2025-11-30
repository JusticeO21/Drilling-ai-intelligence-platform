import { AppSidebar, Header, TabNavigation } from '@/components/layout'
import { ChatWidget } from '@/features/chat'
import { ScrollArea } from '@/components/ui/scroll-area'

interface DashboardLayoutProps {
  children: React.ReactNode
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="h-screen flex flex-col max-w-screen-3xl  mx-auto border">
      <Header />

      <div className="flex-1 flex w-full relative overflow-hidden">
        <AppSidebar />

        <ScrollArea className="flex-1 2xl:max-w-screen-xl mx-auto">
          <div className="flex flex-col bg-white dark:bg-black">
            <TabNavigation />
            {children}
          </div>
        </ScrollArea>

        <ChatWidget />
      </div>
    </div>
  )
}
