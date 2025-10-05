"use client";

import { useState } from "react";
import CsvForm from "@/components/CsvForm";
import ThreeScene from "@/components/ThreeScene";
import Footer from "@/components/Footer";

type PlanetData = {
  pl_name: string;
  rf_probability: number;
};

export default function Home() {
  const [planetData, setPlanetData] = useState<PlanetData[]>([]);
  const [accuracy, setAccuracy] = useState<number | null>(null);

  return (
    <main className="flex flex-col min-h-screen">
      <div className="flex-grow p-6">
        {(planetData?.length ?? 0) > 0 ? (
          <ThreeScene data={planetData} />
        ) : (
          <>
            <CsvForm onPlanetsUpdate={setPlanetData} onAccuracyUpdate={setAccuracy} />
            <h2 className="text-lg font-semibold text-gray-200 mt-4 text-center">
              Current Model Accuracy - {accuracy !== null ? `${accuracy}%` : "#"}
            </h2>
          </>
        )}
      </div>
      <Footer />
    </main>
  );
}
