"use client";
import Image from "next/image";
// next/image is a built-in component in Next.js for optimized image loading
// and rendering. It is installed as npm package with Next.js by default.

async function fetchVideoElements(projectId: string) {
    
    // Call the APIs to fetch project elements
    var response = await fetch(`http://127.0.0.1:8000/api/projects?project_id=${projectId}`, {
      method: "GET",
    });

    var script_id = (await response.json()).script_id;
    var response = await fetch(`http://127.0.0.1:8000/api/scripts?script_id=${script_id}`, {
      method: "GET",
    });

    var scriptContent = (await response.json()).content;
    console.log("Script Content: ", scriptContent);

    var response = await fetch(`http://127.0.0.1:8000/api/scenes?script_id=${script_id}`, {
      method: "GET",
    });
    var scenes = await response.json();
    console.log("Scenes: ", scenes);
    var sceneIds = scenes.map((scene: { id: string }) => scene.id);

    // for each sceneid, get the shots
    const shots = await Promise.all(
      sceneIds.map((id:string) =>
        fetch(`http://127.0.0.1:8000/api/shots?scene_id=${id}`)
          .then(res => res.json())
      )
    );

    console.log("Shots: ", shots);

  }

export default function Home() {
  // Get projectid from session storage

  const projectId = sessionStorage.getItem("projectId")?? "";

  fetchVideoElements(projectId);

  
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

      {[1, 2, 3].map((section) => (
        <details
        key={section}
        className="mb-4 bg-white rounded-lg shadow-sm"
        >
        <summary className="px-4 py-3 font-semibold cursor-pointer select-none">
          Section {section}
        </summary>
        <div className="p-4">
          <textarea
          placeholder="Enter text..."
          className="w-full min-h-[60px] mb-3 rounded border border-gray-300 p-2"
          />
          <div className="flex gap-2">
          {[1, 2, 3].map((img) => (
            <div
            key={img}
            className="w-15 h-15 relative rounded overflow-hidden border border-gray-200"
            >
            {/* Image thumbnail goes here */}
            </div>
          ))}
          </div>
        </div>
        </details>
      ))}
      </div>
      {/* Right fixed preview section */}
      <div className="w-[1000px] border-l border-gray-200 bg-white p-8 box-border sticky top-0 h-screen">
      {/* w-[400px]: Fixed width of 400px */}
      {/* border-l: Left border with default color */}
      {/* bg-white: White background color */}
      {/* p-8: Padding of 2rem (32px) on all sides */}
      {/* box-border: Includes padding and border in the element's total width and height */}
      {/* sticky: Sticks to the top of the viewport when scrolling */}
      {/* top-0: Sticks to the top of the viewport */}
      {/* h-screen: Full height of the screen */}

      <h2 className="mb-6 text-xl font-semibold">Preview</h2>
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
        <span className="text-gray-400">Image Preview</span>
        {/* text-gray-400: Gray color for the text */}
      </div>
      </div>
    </div>

  );
}
