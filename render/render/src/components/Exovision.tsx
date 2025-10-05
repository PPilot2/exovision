"use client";
import { useState } from "react";
import ThreeScene from "./ThreeScene";
interface PlanetData {
  pl_name: string;
  rf_probability: number;
}
export default function Exovision() {
  const [file, setFile] = useState<File | null>(null);
  const [planetData, setPlanetData] = useState<PlanetData[]>([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:5000/predict", {
        method: "POST",
        body: formData,
      });
      const data: PlanetData[] = await res.json(); 
      setPlanetData(data); 
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (planetData.length > 0)
    return <ThreeScene data={planetData} />;

  return (
    <div className="flex flex-col items-center mt-10 gap-4">
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-500 transition"
      >
        {loading ? "Uploading..." : "Upload CSV & Predict"}
      </button>
    </div>
  );
}
