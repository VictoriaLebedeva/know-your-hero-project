import type { FC } from "react";
import { useUserStore } from "../stores/userStore";
import { Link, useLocation, useNavigate } from "react-router-dom"

import { Button } from "@/components/ui/button"
import { toast } from "sonner"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuRadioItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

const Header: FC = () => {

    const user = useUserStore((s) => s.user);
    const userName = user?.name ?? "Stranger";

    const location = useLocation();
    const navigate = useNavigate()

    const handleLogout = async () => {
        try {
            const response = await fetch("/api/auth/logout", {
                method: "POST",
                credentials: "include"
            });
            const data = await response.json()
            if (!response.ok) throw new Error(data.message);
            toast.success("Logout successful!");
            navigate("/");
        } catch (error) {
            toast.error(`Logout failed: ${(error as Error).message}`);
        }
    };

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
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <p className="text-right font-semibold">
                            How are you, <span className="underline">{userName}</span>?
                        </p>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent className="w-56">
                        <DropdownMenuRadioItem value="logout" onClick={handleLogout}>Log Out</DropdownMenuRadioItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </div>
        </div>
    );
}

export default Header;