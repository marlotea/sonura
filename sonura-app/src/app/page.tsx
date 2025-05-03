"use client";
import { useState } from "react";
import { AuroraBackground } from "@/components/ui/aurora-background";
import Link from "next/link";

export default function Home() {
	const [position, setPosition] = useState("50% 50%");
	const backendUrl = "/api";

	const handleMouseMove = (e: React.MouseEvent) => {
		const { clientX, clientY, currentTarget } = e;
		const target = currentTarget as HTMLElement;
		const { offsetWidth, offsetHeight } = target;
		const x = (clientX / offsetWidth) * 100;
		const y = (clientY / offsetHeight) * 100;
		setPosition(`${x}% ${y}%`);
	};

	const handleSpotifyLogin = () => {
		window.location.href = `${backendUrl}/login`;
	};

	return (
		<AuroraBackground>
			<div
				className="h-screen w-full relative overflow-hidden flex flex-col justify-center items-center text-white"
				onMouseMove={handleMouseMove}
			>
				<div className="flex flex-col justify-center items-center">
					<h1>Welcome to Sonura!</h1>

					<button onClick={handleSpotifyLogin}>Login with Spotify</button>

					<button>Continue without connecting account</button>
				</div>
			</div>
		</AuroraBackground>
	);
}
