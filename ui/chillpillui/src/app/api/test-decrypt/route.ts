import { NextRequest, NextResponse } from "next/server";
import { getToken } from "next-auth/jwt";

// Optional: force Node.js runtime (next 13.4+)
export const runtime = "nodejs";

export async function GET(request: NextRequest) {
  console.log("Token decryption endpoint called");
  console.log(process.env.TokenDecryptEndpointEnabled);
  if(process.env.TokenDecryptEndpointEnabled?.toLowerCase() === "false"){
    return NextResponse.json(
      { error: "Token decryption endpoint is disabled" },
      { status: 503 }
    );
  }

  // This will read & decrypt the NextAuth JWE session cookie (or Authorization header)
  const token = await getToken({ req: request, secret: process.env.AUTH_SECRET });

  if (!token) {
    return NextResponse.json(
      { error: "No valid session token found" },
      { status: 401 }
    );
  }

  // Return the decrypted payload as JSON
  return NextResponse.json({ decrypted: token });
}