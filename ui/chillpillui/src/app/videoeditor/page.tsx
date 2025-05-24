"use client";
import Image from "next/image";
import ScriptDetailsBox from "@/components/scriptdetailsbox";
import React, { useState } from "react";
import { useEffect } from "react";  

import Script from "next/script";
// next/image is a built-in component in Next.js for optimized image loading
// and rendering. It is installed as npm package with Next.js by default.

async function fetchVideoElements(
  projectId: string, 
  setScriptContent: React.Dispatch<React.SetStateAction<string>>,
  setScenes: React.Dispatch<React.SetStateAction<never[]>>,) {
    
    // Call the APIs to fetch project elements
    var response = await fetch(`http://127.0.0.1:8000/api/projects?project_id=${projectId}`, {
      method: "GET",
      cache: "no-cache", // Ensure we get the latest data
    });

    var script_id = (await response.json()).script_id;
    console.log(`[${new Date().toISOString()}] Script ID: `, script_id);
    
    var response = await fetch(`http://127.0.0.1:8000/api/scripts?script_id=${script_id}`, {
      method: "GET",
      cache: "no-cache", // Ensure we get the latest data
    });

    var scriptContent = (await response.json()).content;
    console.log(`[${new Date().toISOString()}] Script Content: `, scriptContent);
    setScriptContent(scriptContent);

    var response = await fetch(`http://127.0.0.1:8000/api/scenes?script_id=${script_id}`, {
      method: "GET",
      cache: "no-cache", // Ensure we get the latest data
    });
    var scenes = await response.json();
    console.log(`[${new Date().toISOString()}] Scenes: `, scenes);
    
    scenes = await Promise.all(
      scenes.map(async (scene: { id: string }) => {
        /* Fetch shots for each scene */
        const shotsResponse = await fetch(`http://127.0.0.1:8000/api/shots?scene_id=${scene.id}`, {
          method: "GET",
          cache: "no-cache", // Ensure we get the latest data
        });
        const shots = await shotsResponse.json();
        
        /* Spread the scene object and add shots to it */
        return { ...scene, shots };
      })
    );
    console.log(`[${new Date().toISOString()}] Sceneswithshots: `, scenes);
    setScenes(scenes);

  }

export default function Home() {
  const [scriptContent, setScriptContent] = useState("");
  const [scenes, setScenes] = useState([]);
  const [activeShotText, setActiveShotText] = useState("");

  useEffect(() => {
    // This code runs only once after the component mounts
    // Get projectid from session storage
  const projectId = sessionStorage.getItem("projectId")?? "";
  console.log("Project ID: ", projectId);
  // // Sleep for 3 seconds before fetching video elements
  // setTimeout(() => {
  //   fetchVideoElements(projectId, setScriptContent, setScenes);
  // }, 3000);
  
  fetchVideoElements(projectId, setScriptContent, setScenes);
}, []); // <-- empty array means "run only once"

  
  return (
    // The main page of the video editor 
    // The page is divided into 2 parts
    // The right part is fixed and shows preview of images
    // The left part is scrollable with list of boxes, 
    // each box is expandable and contains a text box
    // and contains another box with array of image thumbnails 

    <div className="flex h-screen">
      {/* flex: Flex for the left and right sections */}
      {/* h-screen: Both sections together use full height of the screen */}

      {/* Left scrollable section */}
      <div className="flex-1 overflow-y-auto p-6 bg-gray-100">
      {/* flex-1: Grows to fill available space, Shrinks if necessary, Starts with a base size of 0%*/}
      {/* overflow-y-auto: Enables vertical scrolling if content overflows */}
      {/* p-6: Padding of 1.5rem (24px) on all sides */}
      {/* bg-gray-100: Light gray background color */}


      <ScriptDetailsBox scriptContent={scriptContent}/>

      {scenes.map((scene:{id:string, content:string, shots:[]}) => (
        <details /* details is a expandable and collapsible box, which expands when it's summary is clicked on*/
        key={scene.id}
        className="mb-4 bg-white rounded-lg shadow-sm"
        >
          {/* Summary is the clickable part of the details element*/}
        <summary className="px-4 py-3 font-semibold cursor-pointer select-none">
          Scene {scene.id}
        </summary>
        <div className="p-4">
          <textarea
          value ={scene.content}
          className="w-full min-h-[60px] mb-3 rounded border border-gray-300 p-2"
          readOnly
          />
          <div className="flex gap-2">
          {scene.shots.map((shot:{id:string, image_prompt:string}) => (
            <div
              key={shot.id}
              className="w-15 h-15 relative rounded overflow-hidden border border-gray-200 cursor-pointer"
              onClick={() => setActiveShotText(shot.image_prompt)}
            >
            </div>
          ))}
          </div>
        </div>
        </details>
      ))}
      </div>
      {/* Right fixed preview section */}
      <div className="w-[600px] border-l border-gray-200 bg-white p-8 box-border sticky top-0 h-screen">
      {/* w-[400px]: Fixed width of 400px */}
      {/* border-l: Left border with default color */}
      {/* bg-white: White background color */}
      {/* p-8: Padding of 2rem (32px) on all sides */}
      {/* box-border: Includes padding and border in the element's total width and height */}
      {/* sticky: Sticks to the top of the viewport when scrolling */}
      {/* top-0: Sticks to the top of the viewport */}
      {/* h-screen: Full height of the screen */}

        <h2 className="mb-6 text-xl font-semibold">Active Shot Details</h2>
        {/* mb-6: Margin bottom of 1.5rem (24px) */}
        {/* text-xl: Font size of 1.25rem (20px) */}
        {/* font-semibold: Semi-bold font weight */}

      {/* Image preview area */}
        <div className="w-full h-[300px] bg-gray-200 rounded-lg flex items-center justify-center">
        {/* w-full: Full width */}
        {/* h-[300px]: Fixed height of 300px */}
        {/* bg-gray-200: Light gray background color */}
        {/* rounded-lg: Rounded corners */}
        {/* flex: Flexbox layout */}
        {/* items-center: Center items inside this div vertically */}
        {/* justify-center: Center items inside this div horizontally */}
          <span className="text-gray-400 mb-2 block">Image Preview</span>
          
          {/* text-gray-400: Gray color for the text */}
        </div>


        <h1 className="mb-6 text-xl font-semibold">Image Prompt</h1>

        <div className="p-4">
        <textarea
            value={activeShotText}
            className="w-full min-h-[60px] mb-3 rounded border border-gray-300 p-2"
            readOnly
          />
        </div>
      </div>
    </div>

  );
}
