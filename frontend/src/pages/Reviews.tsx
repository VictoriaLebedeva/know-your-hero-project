import type { FC } from "react";
import { useEffect, useState } from "react";
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

const Reviews: FC = () => {

    const [reviews, setReviews] = useState<Review[]>([]);

    useEffect(() => {
        fetch("/api/reviews", { credentials: "include" })
            .then(res => res.json())
            .then(data => {
                if (Array.isArray(data)) setReviews(data);
            });

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
