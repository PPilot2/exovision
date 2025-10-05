"use client";
import Footer from "./Footer";
import CsvForm from "./CsvForm";

export default function Start() {
  return (
    <main className="flex flex-col min-h-screen text-center p-4 bg-gray-900 text-gray-200">
      <section className="flex-grow p-6">
        <h1 className="text-[60px] font-extrabold text-blue-400 drop-shadow-lg">
          Exovision
        </h1>

        <a
          className="text-blue-500 font-bold underline hover:text-blue-400 transition-colors"
          target="_blank"
          href="https://www.spaceappschallenge.org/2025/challenges/a-world-away-hunting-for-exoplanets-with-ai/?tab=details"
        >
          A World Away: Hunting for Exoplanets with AI
        </a>

        <p className="m-10 mt-4 text-gray-300 max-w-3xl mx-auto leading-relaxed">
          Challenge - Data from several different space-based exoplanet surveying
          missions have enabled discovery of thousands of new planets outside
          our solar system, but most of these exoplanets were identified manually.
          With advances in artificial intelligence and machine learning (AI/ML),
          it is possible to automatically analyze large sets of data collected by
          these missions to identify exoplanets. Your challenge is to create an
          AI/ML model that is trained on one or more of the open-source exoplanet
          datasets offered by NASA and that can analyze new data to accurately
          identify exoplanets. (Astrophysics Division)
        </p>

        <h2 className="text-lg font-semibold text-gray-200 mt-4">
          Current Model Accuracy - #
        </h2>
      </section>

      <section className="mt-6 flex flex-col items-center">
        <CsvForm />
      </section>

      <Footer />
    </main>
  );
}
