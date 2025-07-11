import type { FC } from "react";
import { useEffect, useState } from "react";
import type { ReviewType } from "@/types/review"
import { fetchAllReviews } from "@/lib/api/reviews";
import { useUser } from "@/lib/queries/useUser";
import { useColleagues } from "@/lib/queries/useColleagues";

import { Link } from "react-router-dom";

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

    //load information about users and collegues
    useUser();
    useColleagues();

    const [reviews, setReviews] = useState<ReviewType[]>([]);
    useEffect(() => {
        fetchAllReviews().then(setReviews).catch(console.error);
    }, []);

    return (
        <div className="flex flex-col min-h-screen px-[75px] pt-[55px] pb-[35px] bg-white">
            <Header />
            <main className="flex-grow flex flex-col items-start mt-8 space-y-[25px]">
                <Link to="/reviews/new">
                    <Button>+ Add Review</Button>
                </Link>
                <Table className="w-full text-left">
                    <TableHeader>
                        <TableRow>
                            <TableHead>Hero</TableHead>
                            <TableHead>Author</TableHead>
                            <TableHead className="text-[#48973E]">Positive</TableHead>
                            <TableHead className="text-[#973E42]">Negative</TableHead>
                            <TableHead>Created At</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {reviews.map((review) => (
                            <TableRow key={review.id}>
                                <TableCell className="font-medium">{review.adresed_name}</TableCell>
                                <TableCell className="font-medium">{review.author_name}</TableCell>
                                <TableCell className="w-[400px] break-words whitespace-normal">{review.positive}</TableCell>
                                <TableCell className="w-[400px] break-words whitespace-normal">{review.negative}</TableCell>
                                <TableCell>
                                    {new Date(review.created_at).toLocaleString("en-US", {
                                        year: "numeric",
                                        month: "long",
                                        day: "numeric",
                                        hour: "2-digit",
                                        minute: "2-digit",
                                        second: "2-digit",
                                        hour12: false
                                    })}
                                </TableCell>

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
