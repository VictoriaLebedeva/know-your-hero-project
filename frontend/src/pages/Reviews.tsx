import { Button } from "@/components/ui/button";
import Header from "@/components/header";
import Footer from "@/components/Footer";
import type { FC } from "react";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
const Reviews: FC = () => {

    return (
        <div className="flex flex-col min-h-screen px-[75px] pt-[55px] pb-[35px] bg-white">
            <div className="flex justify-between items-center w-full">
                <Header />
                <p className="text-right font-semibold">How are you, John Doe?</p>
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
                        <TableRow>
                            <TableCell className="font-medium">Emma Johnson</TableCell>
                            <TableCell>Always supportive!</TableCell>
                            <TableCell>Could improve response time.</TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </main>
            <Footer />
        </div>
    );
};

export default Reviews;


