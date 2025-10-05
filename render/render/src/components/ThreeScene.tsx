"use client";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { OrbitControls, Html } from "@react-three/drei";
import { useRef, useState } from "react";
import * as THREE from "three";
import { Line } from "@react-three/drei";
import Link from "next/link";
// Planet component
function Planet({
  color,
  name,
  probability,
  position,
  isActive,
}: {
  color: string;
  name: string;
  probability: number;
  position: THREE.Vector3;
  isActive: boolean;
}) {
  const meshRef = useRef<THREE.Mesh>(null!);

  // Rotate the planet
  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.x += 0.01;
    }
  });

  // Set scale: active = 1, inactive = 0.6
  const scale = isActive ? 1 : 0.6;

  return (
    <group position={position} scale={[scale, scale, scale]}>
      <mesh ref={meshRef}>
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial color={color} />
      </mesh>

      {/* Line pointing to label */}
      <Line
        points={[
          [0, 1, 0], // top of the planet
          [0, 1.5, 0], // label position
        ]}
        color="white"
        lineWidth={1}
      />

      {/* Label */}
      <Html
        position={[0, 1.5, 0]}
        center
        distanceFactor={10}
        style={{ pointerEvents: "none" }}
      >
        <div
          style={{
            background: "rgba(0, 0, 0, 0.6)",
            color: "white",
            padding: "4px 8px",
            borderRadius: "8px",
            fontSize: "14px",
            whiteSpace: "nowrap",
          }}
        >
          {name} - {probability}
        </div>
      </Html>
    </group>
  );
}

// Planet data
const PLANETS = [
  {
    name: "TOI-XXX",
    color: "#00aaff",
    probability: 0.95,
    position: new THREE.Vector3(0, 0, 0),
  },
  {
    name: "TOI-YYY",
    color: "#ff5533",
    probability: 0.93,
    position: new THREE.Vector3(4, 0, 0),
  },
  {
    name: "TOI-XXY",
    color: "#ffaa00",
    probability: 0.90,
    position: new THREE.Vector3(8, 0, 0),
  },
];

// Camera controller
function CameraController({ target }: { target: THREE.Vector3 }) {
  const { camera } = useThree();

  useFrame(() => {
    // Smoothly move camera to target + offset
    camera.position.lerp(
      new THREE.Vector3(target.x, target.y, target.z + 5),
      0.05
    );
    camera.lookAt(target);
  });

  return null;
}

export default function ThreeScene() {
  const [index, setIndex] = useState(0);

  const nextPlanet = () => setIndex((i) => (i + 1) % PLANETS.length);
  const prevPlanet = () =>
    setIndex((i) => (i - 1 + PLANETS.length) % PLANETS.length);

  return (
    <div className="relative w-full h-screen">
      <Canvas>
        <ambientLight intensity={0.5} />
        <directionalLight position={[2, 2, 2]} />

        {/* Render planets */}
        {PLANETS.map((planet, i) => (
          <Planet
            key={planet.name}
            color={planet.color}
            name={planet.name}
            probability={planet.probability}
            position={planet.position}
            isActive={i === index}
          />
        ))}

        {/* Fly camera to selected planet */}
        <CameraController target={PLANETS[index].position} />

        <OrbitControls
          minDistance={2}
          maxDistance={15}
          target={PLANETS[index].position}
        />
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
        <Link
          href="/"
          className="bg-gray-800 text-white px-4 py-2 rounded-xl hover:bg-gray-700 transition flex items-center justify-center"
        >
          Back to home
        </Link>
      </div>
    </div>
  );
}
