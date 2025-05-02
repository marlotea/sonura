import { AuroraBackground } from "@/components/ui/aurora-background";
import Link from "next/link";

export default function Page() {

    return (
        <AuroraBackground>
            <div className="flex flex-col justify-center items-center h-screen w-full text-white">
                <Link href="/dashboard">
                    Temporary: Go to Dashboard
                </Link>
            </div>
        </AuroraBackground>
    );
}