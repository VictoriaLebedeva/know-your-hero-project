import type { FC } from "react";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

const Reviews: FC = () => {

    type Review = {
        id: number;
        positive: string;
        negative?: string;
        adresed_id: number;
        adresed_name: string;
        author_id: number;
        author_name: string;
        created_at: string;
    };

    const [reviews, setReviews] = useState<Review[]>([]);
    const [userName, setUserName] = useState<string>("");


    useEffect(() => {
        const stored = localStorage.getItem("user");
        if (stored) setUserName(JSON.parse(stored).name);

        fetch("/api/reviews", { credentials: "include" })
            .then(res => res.json())
            .then(data => {
                if (Array.isArray(data)) setReviews(data);
            });

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
            <main className="flex-grow flex flex-col items-start mt-8 space-y-[25px]">
                <Button>+ Add Review</Button>
                <Table className="w-full text-left">
                    <TableHeader>
                        <TableRow>
                            <TableHead>Hero</TableHead>
                            <TableHead>Positive</TableHead>
                            <TableHead>Negative</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {reviews.map((review) => (
                            <TableRow key={review.id}>
                                <TableCell className="font-medium">{review.adresed_name}</TableCell>
                                <TableCell>{review.positive}</TableCell>
                                <TableCell>{review.negative || "—"}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </main>
            <Footer />
        </div>
    );
};

export default Reviews;
