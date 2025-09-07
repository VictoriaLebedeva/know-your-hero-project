import type { FC, ChangeEvent, FormEvent } from "react";
import { useEffect, useState } from "react";
import { useUserStore } from "../stores/userStore";
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
    recipient_id: string | null;
};

const initialFormData = {
    positive: "",
    negative: "",
    recipient_id: null
};

const AddReview: FC = () => {

    const colleagues = useColleagueStore((s) => s.colleagues);
    const user = useUserStore((s) => s.user);
    const isColleague = user?.role === 'colleague';


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
            recipient_id: value,
        }));
    };

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        if (!formData.recipient_id) {
            toast.error("Please select a colleague before submitting");
            return;
        }

        if (isColleague) {
            if (!formData.positive?.trim()) {
                toast.error("Please fill in the positive field");
                return;
            }

            if (formData.positive?.length > 1000) {
                toast.error("Review is too long (more than 1000 characters). Please, be brief :)");
                return;
            }
        } else {
            if (!formData.positive?.trim() && !formData.negative?.trim()) {
                toast.error("Please fill in at least one of 'positive' or 'negative' fields");
                return;
            }

            if (formData.positive?.length > 1000 || formData.negative?.length > 1000) {
                toast.error("Review is too long (more than 1000 characters). Please, be brief :)");
                return;
            }
        }

        let dataToSubmit;

        if (isColleague) {
            dataToSubmit = {
                positive: formData.positive,
                recipient_id: formData.recipient_id
            };
        } else {
            dataToSubmit = {
                ...formData
            };
        }

        try {
            await createReview(dataToSubmit);
            toast.success("Review successfully created!");
            setFormData({
                ...initialFormData
            });

        } catch (error: any) {
            toast.error(`Creation failed: ${error.message}`);
        }
    };

    return (
        <div className="flex flex-col min-h-screen px-4 sm:px-8 lg:px-[75px] pt-6 sm:pt-[55px] pb-6 sm:pb-[35px] bg-white">
            <Header />
            <main className="flex-grow flex flex-col items-center mt-8 sm:mt-12">
                <form onSubmit={handleSubmit} className="w-full max-w-6xl">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
                        <div className="w-full">
                            <p className="text-lg sm:text-xl font-semibold">Step 1</p>
                            <p className="text-base sm:text-xl">Choose colleague</p>
                            <Select value={formData.recipient_id?.toString() ?? ""} onValueChange={handleColleagueChange}>
                                <SelectTrigger className="w-full mt-6 sm:mt-8">
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

                        <div className="w-full">
                            <p className="text-lg sm:text-xl font-semibold">Step 2</p>
                            <p className="text-base sm:text-xl">Write what you think</p>

                            <div className="flex flex-col gap-2 mt-6 sm:mt-8">
                                <p className="inline-flex justify-center bg-[#48973E] text-white text-sm font-medium rounded px-4 py-1 w-fit">
                                    Such a nice person
                                </p>
                                <Textarea
                                    id="positive"
                                    value={formData.positive}
                                    onChange={handleChange}
                                    placeholder="What is good about colleague?"
                                    className="min-h-[120px] resize-none"
                                />
                            </div>

                            {!isColleague && (
                                <div className="flex flex-col gap-2 mt-6 sm:mt-8">
                                    <p className="inline-flex justify-center bg-[#973E42] text-white text-sm font-medium rounded px-4 py-1 w-fit">
                                        But
                                    </p>
                                    <Textarea
                                        id="negative"
                                        value={formData.negative}
                                        onChange={handleChange}
                                        placeholder="Any gossips?"
                                        className="min-h-[120px] resize-none"
                                    />
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Buttons */}
                    <div className="flex flex-wrap justify-end gap-4 mt-10">
                        <Link to="/reviews" className="w-full sm:w-auto">
                            <Button type="button" variant="outline" className="w-full sm:w-auto">Cancel</Button>
                        </Link>
                        <Button type="submit" className="w-full sm:w-auto">Submit</Button>
                    </div>
                </form>
            </main>
            <Footer />
        </div>
    );
};

export default AddReview;