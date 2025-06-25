import type { FC } from "react";
import { useEffect, useState } from "react";
import type { ReviewType } from "../types/review"
import { fetchAllReviews } from "@/lib/api/reviews";

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
                            <TableHead>Positive</TableHead>
                            <TableHead>Negative</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {reviews.map((review) => (
                            <TableRow key={review.id}>
                                <TableCell className="font-medium">{review.adresed_name}</TableCell>
                                <TableCell className="font-medium">{review.author_name}</TableCell>
                                <TableCell>{review.positive}</TableCell>
                                <TableCell>{review.negative}</TableCell>
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
