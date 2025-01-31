import { api } from "../../../api";

interface VerifyEmailProps {
    msg?: string;
    type: "STR" | "PDF" | "TXT";
    file?: File;
}

export async function verifyEmail({ msg, type, file }: VerifyEmailProps) {
    try {
        let response;

        if (type === "STR") {
            response = await api.post("/classifier/answer-mistral", { msg, type });
            console.log(response);
        } else if (file) {
            const formData = new FormData();
            formData.append("msg", file);
            formData.append("type", type);

            response = await api.post("/classifier/answer-mistral", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
        } else {
            throw new Error("Arquivo não encontrado.");
        }

        return response.data;
    } catch (err: any) {
        return err.response?.data || "Erro desconhecido";
    }
}