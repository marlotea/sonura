"use client";

import { useState } from "react";
import Link from "next/link";
import { AuroraBackground } from "@/components/ui/aurora-background";
import { Play, SkipBack, SkipForward } from "phosphor-react";
import { motion, AnimatePresence } from "framer-motion";

const mockCards = [
    { id: 1, title: "Song Title 1", artist: "Artist 1" },
    { id: 2, title: "Song Title 2", artist: "Artist 2" },
    { id: 3, title: "Song Title 3", artist: "Artist 3" },
];


export default function Page() {

    // card swipe logic
    const [cards, setCards] = useState(mockCards);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [direction, setDirection] = useState<"left" | "right" | null>(null);

    const handleSwipe = (dir: "left" | "right") => {
        if (currentIndex < cards.length - 1) {
            setDirection(dir);
            setTimeout(() => {
                setCurrentIndex((prev) => prev + 1);
                setDirection(null);
            }, 300); // Match animation duration
        }
    };

    // settings display logic
    const [showSettings, setShowSettings] = useState(false);

    const toggleSettings = () => {
        setShowSettings((prev) => !prev);
    };

    return (
        <AuroraBackground>
            <div className="h-screen w-full relative overflow-hidden flex flex-col justify-center items-center text-white">

                <div className="flex flex-row w-full h-full justify-between items-center overflow-hidden">

                    <div className="w-3/8 h-full p-16">
                        <Link href="/dashboard">← Return back to dashboard</Link>
                    </div>

                    <div className="overflow-hidden">
                        <AnimatePresence mode="wait">
                            {cards.slice(currentIndex, currentIndex + 1).map((card, index) => (
                                <motion.div key={card.id}
                                            className="bg-white/10 backdrop-blur-md rounded-2xl flex flex-col
                                                        justify-center items-center shadow-xl"
                                            initial={{
                                                opacity: 0,
                                                x: index === 0 ? 0 : direction === "left" ? 200 : -200,
                                                scale: 0.8, }}
                                            animate={{
                                                opacity: 1,
                                                x: 0,
                                                scale: 1, }}
                                            exit={{
                                                opacity: 0,
                                                x: direction === "left" ? -200 : 200,
                                                scale: 0.8, }}
                                            transition={{ duration: .3 }}>
                                    <div className="flex flex-col w-full justify-center p-8">
                                        <div className="w-65 h-65 bg-gray-500 mb-8 rounded-xl"></div>
                                        <p>Song Title</p>
                                        <p>Artist Name</p>
                                        <div className="bg-gray-500 h-0.75 rounded-full my-4"></div>
                                        <div className="flex flex-row justify-center gap-4 mt-4">
                                            <SkipBack size={20} weight="fill"/>
                                            <Play size={20} weight="fill"/>
                                            <SkipForward size={20} weight="fill"/>
                                        </div>
                                    </div>
                                </motion.div>
                            ))}
                        </AnimatePresence>
                    </div>

                    {/* Card */}
                    {/*<div className="bg-white/10 backdrop-blur-md rounded-2xl flex flex-col justify-center items-center shadow-xl">*/}
                    {/*    <div className="flex flex-col w-full justify-center p-8">*/}
                    {/*        <div className="w-65 h-65 bg-gray-500 mb-8 rounded-xl"></div>*/}
                    {/*        <p>Song Title</p>*/}
                    {/*        <p>Artist Name</p>*/}
                    {/*        <div className="bg-gray-500 h-0.75 rounded-full my-4"></div>*/}
                    {/*        <div className="flex flex-row justify-center gap-4 mt-4">*/}
                    {/*            <SkipBack size={20} weight="fill"/>*/}
                    {/*            <Play size={20} weight="fill"/>*/}
                    {/*            <SkipForward size={20} weight="fill"/>*/}
                    {/*        </div>*/}
                    {/*    </div>*/}
                    {/*</div>*/}

                    <div
                        className={`w-3/8 h-full p-16 transform transition-transform duration-500 ${
                            showSettings ? "translate-x-0 opacity-100" : "translate-x-full"
                        }`}
                    >
                        recommendation settings placeholder
                    </div>
                </div>

                <div className="my-10">
                    <button onClick={toggleSettings} className="text-white">
                        Recommendation Settings
                    </button>
                </div>

                <div className="flex gap-4 mb-8">
                    <button
                        onClick={() => handleSwipe("left")}
                        className="px-4 py-2 bg-red-500 rounded-lg"
                    >
                        Swipe Left
                    </button>
                    <button
                        onClick={() => handleSwipe("right")}
                        className="px-4 py-2 bg-green-500 rounded-lg"
                    >
                        Swipe Right
                    </button>
                </div>
            </div>
        </AuroraBackground>
    );
}