import "@/app/globals.css"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

async function getNodeData(node_id:string , date1:string , date2:string) {
    const res = await fetch(`http://localhost:3000/api/${node_id}/${date1}/${date2}/node_data`, { cache: 'no-store' })
    
    if (!res.ok) {
      // This will activate the closest `error.js` Error Boundary
      throw new Error('Failed to fetch data')
    }
   
    return res.json()
  }

  
  
export default async function NodeDataPage({ params }: { params: { node_id: string , date1 : string , date2 : string} }){
    const node_id = params.node_id
    const date1 = params.date1
    const date2 = params.date2
    let node_data = await getNodeData(node_id,date1,date2)
    //console.log(node_data)
    return(
        <div>
            Data for node {node_id} between {date1} and {date2}
            <ScrollArea className="h-[900px]">
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
            </ScrollArea>
        </div>
    )
}