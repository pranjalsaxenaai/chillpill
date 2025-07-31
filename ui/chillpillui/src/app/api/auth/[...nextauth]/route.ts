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
import type { JWT } from "next-auth/jwt";
import type { Account, Session } from "next-auth";

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
  callbacks: {
    /**
     * jwt() runs:
     *  - on initial sign in, with `account` populated
     *  - on subsequent requests, with only `token`
     */
    async jwt({ token, account }:{token: JWT, account: Account|null}) {
      // On first sign in, persist the Google id_token into the JWT
      console.log("JWT callback called");
      if (account?.id_token) {
        token.idToken = account.id_token;
      }
      return token;
    },

    /**
     * session() runs whenever `getSession()` or `useSession()` is called
     */
    async session({ session, token }:{session: Session, token: JWT}) {
      // Expose `idToken` client-side at session.idToken
      session.idToken = (token as JWT & { idToken?: string }).idToken;
      return session;
    },
  },
};
const handler = NextAuth(authoptions);

// This tells Next.js to handle both GET and POST requests under /api/auth/...
export {handler as GET, handler as POST};