"use client";
import Link from "next/link";
import { AuroraBackground } from "@/components/ui/aurora-background";
import { Gear, ShareNetwork } from "phosphor-react";
import { useEffect, useState } from "react";

export default function Page() {
	const backendUrl = "/api"
	const [userData, setUserData] = useState(null);
	const [userTopTracks, setTopTracks] = useState(null);
	const [isLoading, setIsLoading] = useState(true);
	const [error, setError] = useState(null);

	useEffect(() => {
		const fetchUserData = async () => {
	
			try {
				const response = await fetch(`${backendUrl}/spotify/user-data`, {
					credentials: "include",
				});
	
				if (!response.ok) {
					const errorText = await response.text();
					console.error("Fetch failed with response:", errorText);
					throw new Error("Failed to fetch user data");
				}
	
				const data = await response.json();
				setUserData(data.user);
			} catch (err) {
				console.error("Error fetching user data:", err);
				setError(err.message);
			} finally {
				setIsLoading(false);
			}
		};

		const fetchUserTopTracks = async () => {
			try {
				const response = await fetch(`${backendUrl}/spotify/top-tracks/1/10`, {
					credentials: "include"
				});

				if (!response.ok) {
					const errorText = await response.text();
					console.error("Fetch failed with response:", errorText);
					throw new Error("Failed to fetch user top tracks");
				}

				const data = await response.json();
				console.log("Fetched user top tracks:", data);

				setTopTracks(data["top-tracks"]);
				console.log(userTopTracks)
			} catch (err) {
				console.error("Error fetching user top tracks:", err);
				setError(err.message);
			} finally {
				setIsLoading(false);
			}
		}
	
		fetchUserData();
		fetchUserTopTracks();
	}, []);
	

	return (
		<AuroraBackground>
			<div className="h-screen w-full relative overflow-hidden flex flex-col justify-center items-center text-white">
				<div className="w-2/3 h-2/3 bg-white/10 backdrop-blur-md rounded-xl p-4 flex justify-center items-center shadow-xl">
					{/* Opaque Content */}
					<div className="flex flex-col opacity-100 w-full h-full gap-4">
						{/* Top Section: Dashboard Content*/}
						<div className="flex flex-row h-7/8 p-4 gap-4">
							{/* Left Section: Profile */}
							<div className="w-1/4 flex flex-col justify-between">
								{/*  Profile Picture Placeholder  */}
								<div className="flex flex-col items-center gap-2">
								<div className="w-45 h-45 rounded-full bg-gray-300 overflow-hidden">
									{userData?.images?.length > 0 ? (
										<img
											src={userData.images[0].url}
											alt="Profile"
											className="w-full h-full object-cover"
										/>
									) : (
										<div className="w-full h-full bg-gray-300" />
									)}
								</div>
									<p className="bold text-xl">
									{isLoading
										? "Loading..."
										: error
											? "Error loading username"
											: userData
												? userData.display_name
												: "No username"}
								</p>

									<p>[status] connected to Spotify</p>
									<p>your taste:</p>
								</div>

								<div className="flex gap-4 justify-center items-center">
									<Gear />
									<Link href="/settings">settings</Link>
									<ShareNetwork />
									<p>share profile</p>
								</div>
							</div>

							{/* Right Section: Recent Liked Songs, Popular Tracks */}
							<div className="w-3/4 flex flex-col gap-4">
								<div>
									<p>Welcome Back, User!</p>
									<p>You've swiped X songs, liked Y and disliked Z.</p>
									<p>Your favourite styles seem to be P and Q.</p>
								</div>
								<div className="flex flex-row">
									<div className="w-1/2">Recently Liked Songs</div>
									<div className="w-1/2">
								<p className="text-lg font-bold mb-2">Popular Tracks</p>
								{isLoading && <p>Loading tracks...</p>}
								{error && <p>Error loading tracks</p>}
								{userTopTracks && userTopTracks.items && userTopTracks.items.length > 0 ? (
							<ul className="list-disc list-inside space-y-1">
								{userTopTracks.items.map((track, index) => (
								<li key={track.id || index}>
									{track.name} - {track.artists.map(artist => artist.name).join(", ")}
								</li>
								))}
							</ul>
							) : (
							!isLoading && <p>No top tracks found.</p>
							)}
							</div>
								</div>
							</div>
						</div>
						{/* Bottom Section: Button to Swipe Tracks */}
						<div className="flex justify-center items-center">
							<div>
								<Link href="/discover">start swiping songs</Link>
							</div>
						</div>
					</div>
				</div>
			</div>
		</AuroraBackground>
	);
}
