import type { FC, ChangeEvent, FormEvent } from "react";
import { useEffect, useState } from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea"
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"


type Colleague = {
    id: number;
    name: string;
    email: string;
    role: string;
    created_at: string;
};

type CurrentUser = {
    id: number;
    name: string;
    email: string;
    role: string;
    created_at: string;
};

type FormData = {
    positive: string;
    negative: string;
    adresed_id: number | null;
    author_id: number | null;
};

const AddReview: FC = () => {

    const [user, setUser] = useState<CurrentUser | null>(null);
    const [colleagues, setColleagues] = useState<Colleague[]>([]);
    const [formData, setFormData] = useState<FormData>({
        positive: "",
        negative: "",
        adresed_id: null,
        author_id: null,
    });

    // Load user from localStorage
    useEffect(() => {
        const stored = localStorage.getItem("user");
        if (stored) {
            const parsed = JSON.parse(stored);
            setUser(parsed);
        }
    }, []);

    // Load colleagues when component mounts
    useEffect(() => {
        const cached = localStorage.getItem("colleagues");
        if (cached) {
            setColleagues(JSON.parse(cached));
            return;
        }
        fetch("/api/users", { credentials: "include" })
            .then((res) => res.json())
            .then((data) => {
                if (Array.isArray(data)) {
                    setColleagues(data);
                    localStorage.setItem("colleagues", JSON.stringify(data));
                }
            });
    }, []);


    // When user loads, set author_id
    useEffect(() => {
        setFormData((prev) => ({
            ...prev,
            author_id: user?.id ?? null,
        }));
    }, [user]);

    const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
        const { id, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [id]: value,
        }));
    };

    const handleColleagueChange = (value: string) => {
        setFormData((prev) => ({
            ...prev,
            adresed_id: Number(value),
        }));
    };

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        // Update author_id in case user just loaded
        const dataToSubmit = { ...formData, author_id: user?.id ?? null };
        try {
            const response = await fetch("/api/reviews", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(dataToSubmit),
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.message);
            alert("Review successfully created!");
            // Optionally reset form here
        } catch (error) {
            alert(`Creation failed: ${(error as Error).message}`);
        }
    };

    const userName = user?.name ?? "John Doe";

    return (
        <div className="flex flex-col min-h-screen px-[75px] pt-[55px] pb-[35px] bg-white">
            <div className="flex justify-between items-center w-full">
                <Header />
                <div className="relative text-right">
                    <p className="text-right font-semibold">
                        How are you, <span className="underline">{userName}</span>?
                    </p>
                </div>
            </div>
            <main className="flex-grow flex flex-col items-center mt-12">
                <form onSubmit={(e) => handleSubmit(e)} className="form-container">
                    <div className="flex flex-row gap-[70px]">
                        <div className="w-lg">
                            <p className="text-xl font-semibold">Step 1</p>
                            <p className="text-xl">Choose colleague</p>
                            <Select onValueChange={handleColleagueChange}>
                                <SelectTrigger className="w-full mt-8">
                                    <SelectValue placeholder="Select an option" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectGroup>
                                        {colleagues.map((colleague) => (
                                            <SelectItem key={colleague.id} value={colleague.id.toString()}>
                                                {colleague.name}
                                            </SelectItem>
                                        ))}
                                    </SelectGroup>
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="w-lg">
                            <p className="text-xl font-semibold">Step 2</p>
                            <p className="text-xl">Write what you think</p>
                            <div className="flex flex-col gap-[10px] mt-8">
                                <p className="inline-flex w-[200px] justify-center bg-[#48973E] text-white text-sm font-medium rounded px-4 py-1">
                                    Such a nice person
                                </p>
                                <Textarea id="positive" value={formData.positive} onChange={handleChange} placeholder="What is good about collegue?" />
                            </div>
                            <div className="flex flex-col gap-[10px] mt-8">
                                <p className="inline-flex w-[200px] justify-center bg-[#973E42] text-white text-sm font-medium rounded px-4 py-1">
                                    But
                                </p>
                                <Textarea id="negative" value={formData.negative} onChange={handleChange} placeholder="Any gossips?" />
                            </div>
                        </div>
                    </div>
                    <div className="flex flex-row justify-end gap-[10px] mt-10">
                        <Button type="button" variant="outline">Cancel</Button>
                        <Button type="submit">Submit</Button>
                    </div>
                </form>
            </main>
            <Footer />
        </div>
    );
};

export default AddReview;