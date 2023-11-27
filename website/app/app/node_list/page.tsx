//"use client"
import "@/app/globals.css"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
    Collapsible,
    CollapsibleContent,
    CollapsibleTrigger,
} from "@/components/ui/collapsible"
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
  
  async function getNodeList() {
    const res = await fetch('http://localhost:3000/api/node_list', { cache: 'no-store' })
    
    if (!res.ok) {
      // This will activate the closest `error.js` Error Boundary
      throw new Error('Failed to fetch data')
    }
   
    return res.json()
  }

  async function getNodeData(node_id:any) {
    const res = await fetch(`http://localhost:3000/api/${node_id}/node_data`, { cache: 'no-store' })
    
    if (!res.ok) {
      throw new Error('Failed to fetch data')
    }
   
    return res.json()
  }

  async function getNodeIP(node_id:any) {
    const res = await fetch(`http://localhost:3000/api/${node_id}/node_ip`, { cache: 'no-store' })
    
    if (!res.ok) {
      throw new Error('Failed to fetch data')
    }
   
    return res.json()
  }
  
  async function downloadVideo(video_path:string,node_ip:string){

  }

  async function NodeListCollapsible({node_id}:{node_id:any}){
    const [node_data, node_ip] = await Promise.all([getNodeData(node_id), getNodeIP(node_id)]);
    //downloadVideo(data.video,node_ip[0].ip_address)
    //console.log(node_ip[0].ip_address)
    return(
        <Collapsible key={node_id} className="border p-4">
          <CollapsibleTrigger key={node_id}>{node_ip[0].name}</CollapsibleTrigger>
          <CollapsibleContent key={node_id}>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Event ID</TableHead>
                  <TableHead>Animal</TableHead>
                  <TableHead>Date</TableHead>
                  <TableHead>Video</TableHead>
                </TableRow>
              </TableHeader>
            {node_data.map( (data: { event_id: string, animal: string, event_time: string, video: string}) => 
              <TableBody key={node_id}>
                <TableRow key={node_data.event_id}>
                  <TableCell>{data.event_id}</TableCell>
                  <TableCell>{data.animal}</TableCell>
                  <TableCell>{data.event_time}</TableCell>
                  <TableCell>{data.video}</TableCell>
                </TableRow>
              </TableBody>
            )}
            </Table>
          </CollapsibleContent>
        </Collapsible>
    )
  }

export default async function NodeListPage() {
  const node_list = await getNodeList()
  //console.log(node_list)
  
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