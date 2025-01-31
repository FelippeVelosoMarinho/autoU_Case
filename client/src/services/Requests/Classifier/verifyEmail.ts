import { api } from "../../../api";

interface VerifyEmailProps {
    msg?: string;
    type: "STR" | "PDF" | "TXT";
    file?: File;
}

export async function verifyEmail({ msg, type, file }: VerifyEmailProps) {
    try {
        let response;
        console.log(type);

        if (type === "STR") {
            // Enviar texto diretamente para a API correta
            response = await api.post("/classifier/answer-mistral", { msg, type });
        } else if (file) {
            const formData = new FormData();
            formData.append("file", file);

            // Enviar arquivo para a rota específica de documentos
            response = await api.post("/classifier/answer-mistral-docs", formData, {
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
