
import { query } from "@/lib/db";
import { NextRequest, NextResponse } from "next/server";

export async function GET(request : {request:NextRequest},{ params }: { params: { node_id: string } }) {
    const node_id = params.node_id
    const node_data = await query({
        query: `SELECT * FROM nodes WHERE node_id = ${node_id}`,
        values: [],
    });
    
    //console.log(node_data)
    let data = JSON.stringify(node_data);
    return new Response(data, {
        status: 200,
    });
}