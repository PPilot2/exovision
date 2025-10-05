"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function CsvForm() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    } else {
      setFile(null);
    }
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!file) {
      // No file, just navigate to /scene
      router.push("/scene");
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      const csvData = reader.result as string;

      // Pass CSV data as base64 in URL query (optional)
      const encoded = encodeURIComponent(csvData);
      router.push(`/scene?csv=${encoded}`);
    };
    reader.readAsText(file);
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
          Add new CSV data (optional)
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
          className="bg-blue-600 text-white px-6 py-2 rounded-xl font-semibold
                     hover:bg-blue-500 transition-colors w-full"
        >
          Continue
        </button>
      </form>
    </section>
  );
}
