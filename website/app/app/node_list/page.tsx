import "@/app/globals.css"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
    Collapsible,
    CollapsibleContent,
    CollapsibleTrigger,
  } from "@/components/ui/collapsible"
  

export default function NodeListPage() {
    return (
      <div>
        Node List Page
        <ScrollArea className="h-[200px]  rounded-md border p-4">
            <Collapsible>
                <CollapsibleTrigger>Node Name/Number</CollapsibleTrigger>
                <CollapsibleContent>
                    Content for the node
                </CollapsibleContent>
            </Collapsible>
        </ScrollArea>
      </div>
    )
  }
  