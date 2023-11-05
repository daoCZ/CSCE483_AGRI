//"use client"
import "@/app/globals.css"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
    Collapsible,
    CollapsibleContent,
    CollapsibleTrigger,
  } from "@/components/ui/collapsible"
  
  async function getNodeList() {
    const res = await fetch('http://localhost:3000/api/node_list')
   
    if (!res.ok) {
      // This will activate the closest `error.js` Error Boundary
      throw new Error('Failed to fetch data')
    }
   
    return res.json()
  }

  async function getNodeData(node_id:any) {
    const res = await fetch(`http://localhost:3000/api/${node_id}/node_data`)
   
    if (!res.ok) {
      throw new Error('Failed to fetch data')
    }
   
    return res.json()
  }
  
  async function NodeListCollapsible({node_id}:{node_id:any}){
    let node_data = await getNodeData(node_id)
    
    return(
        <Collapsible key={node_id} className="border p-4">
          <CollapsibleTrigger key={node_id}>Node {node_id}</CollapsibleTrigger>
          <CollapsibleContent key={node_id}>
              {node_data[1]}
          </CollapsibleContent>
        </Collapsible>
    )
  }

export default async function NodeListPage() {
  const node_list = await getNodeList()
  //console.log(data)
  
    return (
      <div>
        Node List Page
        <ScrollArea className="h-[900px]">
          {node_list.map( (data: { node_id: any }) => 
            <NodeListCollapsible node_id={data.node_id} key={data.node_id}/>
          )}
        </ScrollArea>
        
      </div>
    )
  }
  /*
  <ScrollArea className="rounded-md border p-4">
  </ScrollArea>
  <Collapsible>
              <CollapsibleTrigger>Node Name/Number</CollapsibleTrigger>
              <CollapsibleContent>
                  Content for the node
              </CollapsibleContent>
            </Collapsible>

            <Collapsible>
              <CollapsibleTrigger>Node Name/Number</CollapsibleTrigger>
              <CollapsibleContent>
                  Content for the node
              </CollapsibleContent>
            </Collapsible>
  */