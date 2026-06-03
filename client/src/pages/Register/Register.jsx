import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "../../components/ui/Button";
import { Input } from "../../components/ui/Input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../../components/ui/Card";
import { toast } from "sonner";
import { subscriptionService } from "../../services/subscriptionService";

const subscriptionSchema = z.object({
  fullName: z.string().min(2, { message: "Họ tên phải có ít nhất 2 ký tự" }),
  email: z.string().email({ message: "Email không hợp lệ" }),
  subjectCode: z.string().optional(),
  subjectName: z.string().optional(),
});

const Register = () => {
  const form = useForm({
    resolver: zodResolver(subscriptionSchema),
    defaultValues: {
      fullName: "",
      email: "",
      subjectCode: "",
      subjectName: "",
    },
  });

  const onSubmit = async (data) => {
    try {
      await subscriptionService.subscribe(data);
      toast.success("Đăng ký thành công!", {
        description: "Bạn sẽ nhận được email khi có danh sách thi mới.",
      });
      form.reset();
    } catch {
      toast.error("Đăng ký thất bại", {
        description: "Vui lòng thử lại sau.",
      });
    }
  };

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-2xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle>Đăng ký theo dõi danh sách thi</CardTitle>
            <CardDescription>
              Nhập thông tin để nhận thông báo khi có danh sách thi mới
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">
                  Họ và tên *
                </label>
                <Input
                  {...form.register("fullName")}
                  placeholder="Nguyễn Văn A"
                  error={form.errors?.fullName?.message}
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Email *
                </label>
                <Input
                  type="email"
                  {...form.register("email")}
                  placeholder="example@duytan.edu.vn"
                  error={form.errors?.email?.message}
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Mã môn học (tùy chọn)
                </label>
                <Input {...form.register("subjectCode")} placeholder="MA001" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Tên môn học (tùy chọn)
                </label>
                <Input
                  {...form.register("subjectName")}
                  placeholder="Toán cao cấp"
                />
              </div>
              <Button type="submit" className="w-full">
                Đăng ký
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Register;
