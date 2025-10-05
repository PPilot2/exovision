/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

type PlanetData = {
  pl_name: string;
  rf_probability: number;
};

export default function CsvForm({
  onPlanetsUpdate,
  onAccuracyUpdate,
}: {
  onPlanetsUpdate: (data: PlanetData[]) => void;
  onAccuracyUpdate: (accuracy: number) => void;
}) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFile(e.target.files?.[0] || null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!file) {
      setError("Please select a CSV file first.");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("http://localhost:5000/predict", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "Something went wrong.");
      }

      const json = await res.json();

      // Extract planets + accuracy
      const planets: PlanetData[] = json.planets || [];
      const accuracy: number = json.accuracy || 0;

      // Save to sessionStorage
      sessionStorage.setItem("planetData", JSON.stringify(planets));
      sessionStorage.setItem("modelAccuracy", String(accuracy));

      // Update parent (optional)
      onPlanetsUpdate(planets);
      onAccuracyUpdate(accuracy);

      // Go to scene page
      router.push("/scene");
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <section className="mt-6 flex flex-col items-center">
      <form
        onSubmit={handleSubmit}
        className="flex flex-col items-center gap-4 bg-gray-800 p-6 rounded-xl shadow-lg w-full max-w-md border border-gray-700"
      >
        <label
          htmlFor="fileinput"
          className="text-gray-300 font-semibold text-lg"
        >
          Add new CSV data
        </label>
        <input
          type="file"
          id="fileinput"
          name="fileinput"
          accept=".csv"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-300
                     file:mr-4 file:py-2 file:px-4
                     file:rounded-full file:border-0
                     file:text-sm file:font-semibold
                     file:bg-blue-600 file:text-white
                     hover:file:bg-blue-500
                     cursor-pointer
                     bg-gray-700 border border-gray-600 rounded-md"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded-xl font-semibold
                     hover:bg-blue-500 transition-colors w-full"
        >
          {loading ? "Processing..." : "Continue"}
        </button>
        {error && <p className="text-red-500 mt-2">{error}</p>}
      </form>
    </section>
  );
}
