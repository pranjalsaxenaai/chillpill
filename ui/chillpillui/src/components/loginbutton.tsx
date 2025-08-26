import { useSession, signIn, signOut } from "next-auth/react";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getUser, createUser } from "@/lib/apiclient";

export default function LoginButton() {
  const { data: session, status } = useSession();
  const router = useRouter();

  const handleNewUser = async (idtoken: any) => {
    try {
      const response = await getUser(idtoken);

      if (response.status === 404) {
        // User not found, treat as new user
        console.log("New user detected");
        // Perform additional setup for new users
        const postUserResponse = await createUser(idtoken);
        if (!postUserResponse.ok) {
          throw new Error(`API error while creating New User: ${postUserResponse.status}`);
        }
        console.log("New user created");
        // Perform any additional setup for the new user here

        return true;
      }

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      const data = await response.json();   // Use this data to store user info if needed
      return false; // Existing user
    } catch (error) {
      throw new Error(`Error while handling new user: ${error}`);
    }
  };


  useEffect(() => {
    if (session) {
      handleNewUser(session.idToken).catch((error) => {
        console.error("Error handling new user:", error);
        signOut(); // Sign out on error
        router.push("/login"); // Redirect to login on error
      });
      router.push("/project"); // Redirect to project page after login
    }
  }, [session, router]);

  if (status === "loading") {
    return <div>Loading...</div>;
  }

  if (session) {
    return (
      <div>
        Signed in as {session.user?.name || session.user?.email} <br />
        <button onClick={() => signOut()}>Sign out</button>
      </div>
    );
  }

  return (
    <div>
      Not signed in <br />
      <button onClick={() => signIn("google")}>Sign in with Google</button>
    </div>
  );
}