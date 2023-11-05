import { query } from "@/lib/db";
import { NextRequest, NextResponse } from "next/server";

export async function GET(request : {request:NextRequest},response:{response:NextResponse}, { params }: { params: { node_id: string } }) {
    const node_id = params.node_id
    const node_data = await query({
        query: `SELECT * FROM events WHERE node_id = ${node_id}`,
        values: [],
    });

    let data = JSON.stringify(node_data);
    return new Response(data, {
        status: 200,
    });
}