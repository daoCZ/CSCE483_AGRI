import { query } from "@/lib/db";
import { NextRequest, NextResponse } from "next/server";

export async function GET() {
    const node_list = await query({
        query: "SELECT DISTINCT node_id FROM events",
        values: [],
    });

    let data = JSON.stringify(node_list);
    console.log(data)
    return new Response(data, {
        status: 200,
    });
}