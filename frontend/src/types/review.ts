export type ReviewType = {
    id: number;
    positive: string;
    negative?: string;
    adresed_id: number;
    adresed_name: string;
    author_id: number;
    author_name: string;
    created_at: string;
};