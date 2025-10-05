"use client";
import { useState, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls, Html } from "@react-three/drei";
import * as THREE from "three";
import { useRouter } from "next/navigation";

type PlanetData = {
  pl_name: string;
  rf_probability: number;
};

type ThreeSceneProps = {
  data?: PlanetData[];
};

const colors = [
  "#ff4c4c",
  "#4cff4c",
  "#4c4cff",
  "#ffff4c",
  "#ff4cff",
  "#4cffff",
  "#ff924c",
];

function Planet({
  planet,
  isActive,
  color,
}: {
  planet: PlanetData;
  isActive: boolean;
  color: string;
}) {
  const meshRef = useRef<THREE.Mesh>(null!);

  useFrame(() => {
    if (meshRef.current && isActive) {
      meshRef.current.rotation.x += 0.01;
      meshRef.current.rotation.y += 0.005;
    }
  });

  return (
    <group>
      <mesh ref={meshRef}>
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial color={color} />
      </mesh>

      <Html
        position={[0, 1.5, 0]}
        center
        distanceFactor={10}
        style={{ pointerEvents: "none" }}
      >
        <div
          style={{
            background: "rgba(0,0,0,0.7)",
            color: "white",
            padding: "4px 8px",
            borderRadius: "8px",
            fontSize: "14px",
            whiteSpace: "nowrap",
          }}
        >
          <div>Name: {planet.pl_name}</div>
          <div>Probability: {planet.rf_probability.toFixed(2)}</div>
        </div>
      </Html>
    </group>
  );
}

export default function ThreeScene({ data }: ThreeSceneProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const router = useRouter();

  if (!data || data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-screen text-white">
        <p>No planets loaded yet.</p>
        <button
          onClick={() => router.push("/")}
          className="mt-4 bg-gray-800 px-4 py-2 rounded-xl hover:bg-gray-700 transition"
        >
          🔙 Back to Upload
        </button>
      </div>
    );
  }

  const prevPlanet = () =>
    setCurrentIndex((prev) => (prev > 0 ? prev - 1 : data.length - 1));
  const nextPlanet = () =>
    setCurrentIndex((prev) => (prev < data.length - 1 ? prev + 1 : 0));
  // Remove duplicate planets by name
  const uniquePlanets = data.filter(
    (planet, index, self) =>
      index === self.findIndex((p) => p.pl_name === planet.pl_name)
  );

  return (
    <div className="relative w-full h-screen">
      <Canvas camera={{ position: [0, 0, 8] }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[2, 2, 2]} />
        <OrbitControls minDistance={2} maxDistance={12} />

        {uniquePlanets.map((planet, idx) => (
          <group
            key={`${planet.pl_name}-${idx}`}
            position={[(idx - currentIndex) * 3, 0, 0]}
          >
            <Planet
              planet={planet}
              isActive={idx === currentIndex}
              color={colors[idx % colors.length]}
            />
          </group>
        ))}
      </Canvas>

      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex gap-4">
        <button
          onClick={prevPlanet}
          className="bg-gray-800 text-white px-4 py-2 rounded-xl hover:bg-gray-700 transition"
        >
          ⬅️ Previous
        </button>
        <button
          onClick={nextPlanet}
          className="bg-gray-800 text-white px-4 py-2 rounded-xl hover:bg-gray-700 transition"
        >
          Next ➡️
        </button>
        <button
          onClick={() => router.push("/")}
          className="bg-gray-800 text-white px-4 py-2 rounded-xl hover:bg-gray-700 transition"
        >
          🔙 Back to Upload
        </button>
      </div>
    </div>
  );
}
