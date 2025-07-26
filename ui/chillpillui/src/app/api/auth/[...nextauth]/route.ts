// Any file under pages/api is treated as an API endpoint instead of a React page.
// Any file under pages is server side
// pages/api/auth/[...nextauth].ts sets up NextAuth.js for authentication.
// It creates a catch-all route for authentication-related requests.

// All the following routes will be handled by this file:
// - GET /api/auth/signin
// - POST /api/auth/callback/google
// - GET /api/auth/signout
// - GET /api/auth/session



import NextAuth, { SessionStrategy } from "next-auth";
import GoogleProvider from "next-auth/providers/google";

export const authoptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
    }),
  ],
  session: {
    strategy: "jwt" as SessionStrategy,
  },
};
const handler = NextAuth(authoptions);

// This tells Next.js to handle both GET and POST requests under /api/auth/...
export {handler as GET, handler as POST};