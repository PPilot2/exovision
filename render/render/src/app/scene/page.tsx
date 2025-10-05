"use client";
import { useEffect, useState } from "react";
import ThreeScene from "@/components/ThreeScene";
import Link from "next/link";
type PlanetData = {
  pl_name: string;
  rf_probability: number;
};
export default function ScenePage() {
  const [planetData, setPlanetData] = useState<PlanetData[]>([]);

  useEffect(() => {
    const stored = sessionStorage.getItem("planetData");
    if (stored) {
      setPlanetData(JSON.parse(stored));
    }
  }, []);

  return (
    <main className="h-screen">
      {planetData.length > 0 ? (
        <ThreeScene data={planetData} />
      ) : (
        <div className="text-center text-gray-300 mt-20">
          <p>No planets loaded yet.</p>
          <Link
            href="/"
            className="inline-block mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-500 transition"
          >
            🔙 Back to Upload
          </Link>
        </div>
      )}
    </main>
  );
}
