export type ReviewType = {
    id: number;
    positive: string;
    negative?: string;
    adresed_id: string;
    adresed_name: string;
    author_id: string;
    author_name: string;
    created_at: string;
};