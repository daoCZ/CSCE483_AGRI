import { query } from "@/lib/db";

export async function GET(request : {request:any}) {
    const node_list = await query({
        query: "SELECT DISTINCT node_id FROM events",
        values: [],
    });

    let data = JSON.stringify(node_list);
    return new Response(data, {
        status: 200,
    });
}