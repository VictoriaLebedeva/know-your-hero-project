import type { FC, ChangeEvent, FormEvent } from "react";
import { useEffect, useState } from "react";
import { useUserStore } from "../stores/userStore";
import { useColleagues } from "../lib/queries/useColleagues";
import { useColleagueStore } from "../stores/colleagueStore";
import { createReview } from "@/lib/api/reviews";

import { Link } from "react-router-dom"

import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea"
import { toast } from "sonner"
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"

type FormData = {
    positive: string;
    negative: string;
    adresed_id: number | null;
    author_id: number | null;
};

const initialFormData = {
    positive: "",
    negative: "",
    adresed_id: null,
    author_id: null,
};

const AddReview: FC = () => {

    useColleagues();
    const colleagues = useColleagueStore((s) => s.colleagues);
    const user = useUserStore((s) => s.user);

    const [formData, setFormData] = useState<FormData>(initialFormData)

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
        if (!formData.positive?.trim() && !formData.negative?.trim()) {
            toast.error("Please fill in at least one of 'positive' or 'negative' fields.");
            return;
        }
        const dataToSubmit = { ...formData, author_id: user?.id ?? null };
        try {
            await createReview(dataToSubmit);
            toast("Review successfully created!");
            setFormData({
                ...initialFormData,
                author_id: user?.id ?? null,
            });
        } catch (error) {
            toast.error(`Creation failed: ${(error as Error).message}`);
        }
    };

    return (
        <div className="flex flex-col min-h-screen px-[75px] pt-[55px] pb-[35px] bg-white">
            <Header />
            <main className="flex-grow flex flex-col items-center mt-12">
                <form onSubmit={(e) => handleSubmit(e)} className="form-container">
                    <div className="flex flex-row gap-[70px]">
                        <div className="w-lg">
                            <p className="text-xl font-semibold">Step 1</p>
                            <p className="text-xl">Choose colleague</p>
                            <Select value={formData.adresed_id?.toString() ?? ""} onValueChange={handleColleagueChange}>
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
                        <Link to="/reviews">
                            <Button type="button" variant="outline">Cancel</Button>
                        </Link>
                        <Button type="submit">Submit</Button>
                    </div>
                </form>
            </main>
            <Footer />
        </div>
    );
};

export default AddReview;