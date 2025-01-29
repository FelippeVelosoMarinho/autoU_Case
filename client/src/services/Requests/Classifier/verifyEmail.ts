import { api } from "../../../api";

type DocType = {
    STR: string;
    PDF: string;
    TXT: string;
}

interface VerifyEmailProps {
    msg?: string;
    type: DocType;
}

export async function verifyEmail(body: VerifyEmailProps) {
    try {
        await api.post("/classifier/answer", body);
    } catch (err: any) {
        return err.response.data
    }
}