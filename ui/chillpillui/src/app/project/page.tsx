"use client";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import Image from "next/image";
// next/image is a built-in component in Next.js for optimized image loading
// and rendering. It is installed as npm package with Next.js by default.

import TriggerOrWaitingButton from "@/components/triggerorwaitingbutton";
import { TriggerOrWaitingButtonState } from "@/components/triggerorwaitingbutton";

export default function Home() {

  const [projectIdea, setProjectIdea] = React.useState("");
  const [projectTitle, setProjectTitle] = React.useState("");
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === "loading") return; // Wait for session to load
    if (!session) {
      router.push("/login"); // Redirect to login if not authenticated
    }
  }, [session, status, router]);

  // Optionally, show a loading spinner while checking session
  if (status === "loading" || !session) {
    return <div>Loading...</div>;
  }

  async function generateProjectElements(
    projectTitle: string, 
    projectIdea: string, 
    setIconState: React.Dispatch<React.SetStateAction<TriggerOrWaitingButtonState>>) {

    // Call the API to generate project elements
    console.log("Generating project elements...");
    console.log("projectTitle: ", projectTitle);
    console.log("projectIdea: ", projectIdea);

    var operationId = await triggerProjectElementsGeneration(projectTitle, projectIdea, );
    console.log("operationId: ", operationId);

    setIconState(TriggerOrWaitingButtonState.Waiting);

    while(!await getProjectElementsGenerationStatus(operationId)){
      console.log("Waiting for project elements generation...");
      await new Promise((resolve) => setTimeout(resolve, 2000));
    }

    console.log("Project elements generated");
    return "681796fabbb5d812dc05649e";
  }

  
  async function triggerProjectElementsGeneration(projectTitle: string, projectIdea: string) {
    
    // Call the API to generate project elements
    var response = await fetch("http://127.0.0.1:8000/api/operations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${session?.idToken}`, // Use session token for authentication
      },
      body: JSON.stringify({
        project_id: "681796fabbb5d812dc05649e",
        project_idea: projectIdea,
        operation_name: "generate_script"
      }),
    });

    var jsonResponse = await response.json();

    return jsonResponse.operation_id;
  }

  async function getProjectElementsGenerationStatus(operationId: string) {
    
    // Call the API to generate project elements
    var response = await fetch(`http://127.0.0.1:8000/api/operations?operation_id=${operationId}`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${session?.idToken}`, // Use session token for authentication
      },
    });

    var jsonResponse = await response.json();
    console.log(`[${new Date().toISOString()}] status: `, jsonResponse.status);
    return jsonResponse.status === "SUCCESS" ? true : false;
  }


  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        {/* Input box for project name */}
        <label className="flex flex-col gap-2 w-full max-w-xs">
          <span className="text-base font-medium">Project name</span>
          <input
            value = {projectTitle}
            onChange={(e) => setProjectTitle(e.target.value)}
            type="text"
            placeholder="Enter project name"
            className="border border-gray-300 dark:border-gray-700 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-black text-black dark:text-white"
          />
        </label>

        {/* Large Input box for project Idea */}
        <label className="flex flex-col gap-2 w-full max-w-xs">
          <span className="text-base font-medium">Project Idea</span>
          <textarea
            value = {projectIdea}
            onChange={(e) => setProjectIdea(e.target.value)}
            placeholder="Enter project idea (Max 500 words)"
            className="border border-gray-300 dark:border-gray-700 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-black text-black dark:text-white"
            rows={4}
          />
        </label>

        <div className="flex gap-4 items-center flex-col sm:flex-row">
          <TriggerOrWaitingButton
            text="Generate Project"
            onClick= {
              async (setIconState) => {
                // Disable the input boxes
                var projectId = await generateProjectElements(projectTitle, projectIdea, setIconState);
                console.log("Redirecting to video page with projectId: ", projectId);

                // Save the projectId to session storage
                sessionStorage.setItem("projectId", projectId);

                // Redirect to the video page
                router.push("/videoeditor");
              }
            }
          />
        </div>
      </main>
      
    </div>
  );
}
