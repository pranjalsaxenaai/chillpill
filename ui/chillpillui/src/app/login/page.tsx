"use client";
import React from "react";
import { useRouter } from "next/navigation";
import LoginButton from "@/components/loginbutton"; // Adjust path if needed

export default function Home() {
  const router = useRouter();

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
      }}
    >
      <LoginButton />
    </div>
  );
}
