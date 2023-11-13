
import { query } from "@/lib/db";
import { NextRequest, NextResponse } from "next/server";

export async function GET(request : {request:NextRequest},{ params }: { params: { node_id: string , date1 : string , date2 : string} }) {
    const node_id = params.node_id
    const date1 = params.date1
    const date2 = params.date2
    const node_data = await query({
        query: `SELECT * FROM events 
        WHERE node_id = '${node_id}'
        AND event_time BETWEEN '${date1}' AND '${date2}'`,
        values: [],
    });
    
    let data = JSON.stringify(node_data);
    return new Response(data, {
        status: 200,
    });
}