import type { FC } from "react";
import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom"
import { Button } from "@/components/ui/button";


type CurrentUser = {
    id: number;
    name: string;
    email: string;
    role: string;
    created_at: string;
}

const Header: FC = () => {
    const [user, setUser] = useState<CurrentUser | null>(null);
    const location = useLocation();

    useEffect(() => {
        const stored = localStorage.getItem("user");
        if (stored) {
            const parsedUser = JSON.parse(stored);
            setUser(parsedUser);
        }
    }, []);

    const userName = user?.name ?? "Stranger";

    return (
        <div className="flex justify-between items-center w-full">
            {location.pathname == "/reviews/new" && (
                <Link to="/reviews" className="absolute top-[85px] left-[15px]">
                    <Button variant="ghost" size="icon">
                        <img src="/arrow-left.png" alt="Back" />
                    </Button>
                </Link>
            )}
            <h1 className="top-5 left-8 text-3xl font-bold leading-none whitespace-pre-line text-left header-font-mono">
                {"Know\nYour\nHero"}
            </h1>
            <div className="relative text-right">
                <p className="text-right font-semibold">
                    How are you, <span className="underline">{userName}</span>?
                </p>
            </div>
        </div>
    );
}


export default Header;
