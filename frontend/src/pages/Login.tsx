import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { toast } from "sonner"
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import type { FC } from "react";
import { useState } from "react";
import Footer from "@/components/Footer";
const Login: FC = () => {

    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData((prevData) => ({
            ...prevData,
            [e.target.id]: e.target.value.trim(),
        }));
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        try {
            const response = await fetch("/api/auth/login", {
                method: "POST",
                credentials: 'include',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email: formData.email,
                    password: formData.password,
                }),
            });
            const data = await response.json()
            if (!response.ok) throw new Error(data.message);

            // get user data
            const meRes = await fetch("/api/me", { credentials: "include" });
            if (!meRes.ok) throw new Error("Could not fetch user data");
            const userData = await meRes.json();

            // save user data into the local storage
            localStorage.setItem("user", JSON.stringify(userData));

            toast("Login successful!");
            navigate("/reviews");
        } catch (error) {
            toast(`Login failed: ${(error as Error).message}`);
        }
    };

    return (
        <div className="flex flex-col min-h-screen px-[75px] pt-[55px] pb-[35px] bg-white">
            <h1 className="top-5 left-8 text-3xl font-bold leading-none whitespace-pre-line text-left header-font-mono">
                {"Know\nYour\nHero"}
            </h1>
            <div className="w-full flex flex-grow justify-center items-center">
                <div className="w-full max-w-md space-y-6 text-center">
                    <h2 className="text-xl font-semibold">Sign In</h2>
                    <form onSubmit={(e) => handleSubmit(e)} className="space-y-4 mt-16">
                        <div className="space-y-2">
                            <Label htmlFor="email">Email</Label>
                            <Input id="email" type="email" placeholder="yourname@example.com" required onChange={handleChange} />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="password">Password</Label>
                            <Input id="password" type="password" placeholder="Password" required onChange={handleChange} />
                        </div>
                        <p className="text-sm text-zinc-500">Don't have an account? <Link className="underline" to="/register">Sign Up</Link></p>
                        <Button type="submit" className="mt-8 w-[85px] h-[40px] bg-primary text-white text-sm rounded-md">
                            Sign In
                        </Button>
                    </form>
                </div>
            </div>
            <Footer />
        </div>
    );
};

export default Login