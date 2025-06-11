import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import type { FC } from "react";

const Register: FC = () => {
  return (
    <div className="flex min-h-screen items-center justify-center bg-white">
      <div className="w-full max-w-md space-y-6 text-center">
        <h1 className="text-3xl font-bold">Know Your Hero</h1>
        <h2 className="text-xl font-semibold">Create an account</h2>
        <form className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" placeholder="yourname@example.com" required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="name">Full Name</Label>
            <Input id="name" type="text" placeholder="John Doe" required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input id="password" type="password" placeholder="Password" required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="repeat-password">Repeat Password</Label>
            <Input id="repeat-password" type="password" placeholder="Repeat password" required />
          </div>
          <Button className="w-full bg-blue-700 text-white">Sign Up</Button>
        </form>
      </div>
    </div>
  );
};

export default Register;