import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import type { FC } from "react";
import { useState } from "react";

const Register: FC = () => {

  const [formData, setFormData] = useState({
    email: "",
    name: "",
    password: "",
    repeatPassword: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prevData) => ({
      ...prevData,
      [e.target.id]: e.target.value.trim(),
    }));
  };


  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (formData.password !== formData.repeatPassword) {
      alert("Passwords do not match. Check");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          name: formData.name,
        }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.message);
      alert("Registration successful!");
    } catch (error) {
      alert(`Registration failed: ${(error as Error).message}`);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-white">
      <div className="w-full max-w-md space-y-6 text-center">
        <h1 className="absolute top-5 left-8 text-3xl font-bold leading-none whitespace-pre-line text-left header-font-mono">
          {"Know\nYour\nHero"}
        </h1>
        <h2 className="text-xl font-semibold">Create an account</h2>
        <form onSubmit={(e) => handleSubmit(e)} noValidate className="space-y-4 mt-16">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" placeholder="yourname@example.com" required onChange={handleChange} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="name">Full Name</Label>
            <Input id="name" type="text" placeholder="John Doe" required onChange={handleChange} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input id="password" type="password" placeholder="Password" required onChange={handleChange} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="repeat-password">Repeat Password</Label>
            <Input id="repeatPassword" type="password" placeholder="Repeat password" required onChange={handleChange} />
          </div>
          <Button type="submit" className="mt-8 w-[85px] h-[40px] bg-primary text-white text-sm rounded-md">
            Sign Up
          </Button>
        </form>
        <img src=".\public\icons8-hero-96.png" alt="Logo" className="absolute bottom-5 right-8 w-12 h-auto" />
      </div>
    </div>
  );
};

export default Register;