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

    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [reviews, setReviews] = useState<ReviewType[]>([]);

    useEffect(() => {
        let mounted = true;
        setIsLoading(true);
        setError(null);

        fetchAllReviews()
            .then((data) => {
                if (!mounted) return;
                setReviews(data);
            })
            .catch((e) => {
                if (!mounted) return;
                console.error(e);
                setError("Can't load reviews");
            })
            .finally(() => {
                if (!mounted) return;
                setIsLoading(false);
            });

        return () => {
            mounted = false;
        };
    }, []);

    return (
        <div className="flex flex-col min-h-screen px-[75px] pt-[55px] pb-[35px] bg-white">
            <Header />
            <main className="flex flex-grow flex-col items-start mt-8 space-y-[25px]">
                <Link to="/reviews/new">
                    <Button>+ Add Review</Button>
                </Link>

                {/* Loader */}
                {isLoading && (
                    <div className="flex flex-col items-center justify-center w-full flex-1">
                        <div className="h-10 w-10 animate-spin rounded-full border-4 border-gray-300 border-t-gray-600" />
                        <p className="mt-3 text-m font-semibold">Loading...</p>
                    </div>
                )}

                {/* Error */}
                {!isLoading && error && (
                    <div className="flex flex-col items-center justify-center w-full flex-1">
                        <p className="text-m font-semibold text-red-600">{error}</p>
                        <Button className="mt-3" onClick={() => {
                            setIsLoading(true);
                            setError(null);
                            fetchAllReviews()
                                .then(setReviews)
                                .catch(() => setError("Can't load reviews"))
                                .finally(() => setIsLoading(false));
                        }}>
                            Retry
                        </Button>
                    </div>
                )}

                {/* No reviews */}
                {!isLoading && !error && reviews.length === 0 && (
                    <div className="flex flex-col items-center justify-center w-full flex-1">
                        <img
                            src="\sad-sitting-svgrepo-com.svg"
                            alt="No reviews"
                            className="w-16 h-16"
                        />
                        <p className="text-m font-semibold">No reviews</p>
                    </div>
                )}

                {/* Reviews */}
                {!isLoading && !error && reviews.length > 0 && (
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
                                    <TableCell className="font-medium">
                                        {review.recipient_name}
                                    </TableCell>
                                    <TableCell className="font-medium">
                                        {review.author_name}
                                    </TableCell>
                                    <TableCell className="w-[400px] break-words whitespace-normal">
                                        {review.positive}
                                    </TableCell>
                                    <TableCell className="w-[400px] break-words whitespace-normal">
                                        {review.negative}
                                    </TableCell>
                                    <TableCell>
                                        {new Date(review.created_at).toLocaleString("en-US", {
                                            year: "numeric",
                                            month: "long",
                                            day: "numeric",
                                            hour: "2-digit",
                                            minute: "2-digit",
                                            second: "2-digit",
                                            hour12: false,
                                        })}
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                )}
            </main>
            <Footer />
        </div>
    );
};

export default Reviews;
