import type { FC } from "react";
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
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"

const AddReview: FC = () => {

    const [userName, setUserName] = useState<string>("");
    useEffect(() => {
        const stored = localStorage.getItem("user");
        if (stored) setUserName(JSON.parse(stored).name);
    }, []);

    return (
        <div className="flex flex-col min-h-screen px-[75px] pt-[55px] pb-[35px] bg-white">
            <div className="flex justify-between items-center w-full">
                <Header />
                <div className="relative text-right">
                    <p className="text-right font-semibold">
                        How are you, <span className="underline">{userName || "John Doe"}</span>?
                    </p>
                </div>
            </div>
            <main className="flex-grow flex flex-col items-center mt-12">
                <form className="form-container">
                    <div className="flex flex-row gap-[70px]">
                        <div className="w-lg">
                            <p className="text-xl font-semibold">Step 1</p>
                            <p className="text-xl">Choose colleague</p>
                            <Select>
                                <SelectTrigger className="w-full mt-8">
                                    <SelectValue placeholder="Select an option" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectGroup>
                                        <SelectLabel>Fruits</SelectLabel>
                                        <SelectItem value="apple">Apple</SelectItem>
                                        <SelectItem value="banana">Banana</SelectItem>
                                        <SelectItem value="blueberry">Blueberry</SelectItem>
                                        <SelectItem value="grapes">Grapes</SelectItem>
                                        <SelectItem value="pineapple">Pineapple</SelectItem>
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
                                <Textarea placeholder="What is good about collegue?" />
                            </div>
                            <div className="flex flex-col gap-[10px] mt-8">
                                <p className="inline-flex w-[200px] justify-center bg-[#973E42] text-white text-sm font-medium rounded px-4 py-1">
                                    But
                                </p>
                                <Textarea placeholder="Any gossips?" />
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