export type ReviewType = {
    id: number;
    positive: string;
    negative?: string;
    recipient_id: string;
    recipient_name: string;
    author_id: string;
    author_name: string;
    created_at: string;
};