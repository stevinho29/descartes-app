import { useForm } from 'react-hook-form';
import { useNavigate, useParams } from 'react-router-dom'
import './portfolio_form.css';
import z, { minLength } from 'zod';
import { zodResolver } from "@hookform/resolvers/zod";
import { Form, FormItem, FormLabel, FormControl, FormMessage, FormField } from "./components/ui/form"
import { Input } from "./components/ui/input"
import { Textarea } from "./components/ui/textarea"
import { createContact, getContact, updateContact } from './api/contact-api';
import { useEffect, useState } from 'react';
import { Button } from './components/ui/button';
import { ContactModel } from './models/contact';

const defaultValues = {
    first_name: "",
    last_name: "",
    email: "",
    job: "",
    comment: ""
}

function PortfolioForm() {

    let { contactId } = useParams();
    let editing = contactId ? true : false;
    const navigate = useNavigate();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [contact, setContact] = useState<ContactModel | undefined>(undefined)
    const contactFormSchema = z.object({
        first_name: z.string().min(2).max(50),
        last_name: z.string().min(2).max(50),
        email: z.email(),
        job: z.string().min(2).max(50),
        comment: z.string().min(1).max(2000)
    })

    type contactFormValues = z.infer<typeof contactFormSchema>

    const contactForm = useForm<contactFormValues>({
        resolver: zodResolver(contactFormSchema),
        defaultValues: defaultValues
    })

    useEffect(() => {
        if (contactId) {
            getContact(contactId).then(res => {
                setContact(res)
                contactForm.setValue("first_name", res.first_name)
                contactForm.setValue("last_name", res.last_name)
                contactForm.setValue("email", res.email)
                contactForm.setValue("job", res.job)
                contactForm.setValue("comment", res.comment)
            }).catch(err => console.log(err))
        }
    }, [contactId, contactForm])

    const onSubmit = async function (params: contactFormValues) {
        if (contactId) {
            updateContact(contactId, params).then(res => {
                navigate("/summary")
            }).catch(err => console.log(err)).finally(() => setIsSubmitting(false))
        } else {
            createContact(params).then(res => {
                navigate("/summary")
            }).catch(err => console.log(err)).finally(() => setIsSubmitting(false))
        }
    }

    const showForm = () => {
        if (contactId) {
            if (contact)
                return true
            return false
        }
        return true
    }
    return (
        <div className="PortfolioForm">
            <p>
                Welcome to the portfolio form
            </p>
            <p><a href="/" className="underline">Take me back home!</a></p>

            <div className="max-w-7xl mx-auto m-4 p-10">

                {showForm() ?
                    <>
                        {editing ? <h1>Update contact form</h1> : <h1>Create contact form</h1>}
                        <Form {...contactForm}>
                            <form onSubmit={contactForm.handleSubmit(onSubmit)}>
                                <FormField
                                    control={contactForm.control}
                                    name="first_name"
                                    render={({ field }) => (
                                        <FormItem className="my-2">
                                            <FormLabel>first name</FormLabel>
                                            <FormControl>
                                                <Input placeholder="Eric" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <FormField
                                    control={contactForm.control}
                                    name="last_name"
                                    render={({ field }) => (
                                        <FormItem className="my-2">
                                            <FormLabel>last name</FormLabel>
                                            <FormControl>
                                                <Input placeholder="Dupont" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <FormField
                                    control={contactForm.control}
                                    name="email"
                                    render={({ field }) => (
                                        <FormItem className="my-2">
                                            <FormLabel>Email</FormLabel>
                                            <FormControl>
                                                <Input placeholder="contact@test.com" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <FormField
                                    control={contactForm.control}
                                    name="job"
                                    render={({ field }) => (
                                        <FormItem className="my-2">
                                            <FormLabel>Job</FormLabel>
                                            <FormControl>
                                                <Input placeholder="Engineer" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <FormField
                                    control={contactForm.control}
                                    name="comment"
                                    render={({ field }) => (
                                        <FormItem className="my-2">
                                            <FormLabel>Comment</FormLabel>
                                            <FormControl>
                                                <Textarea placeholder="Add a comment" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <Button
                                    type="submit"
                                    variant="outline"
                                    disabled={isSubmitting}
                                >
                                    Soumettre
                                </Button>
                            </form>
                        </Form> </> : <div> Loading </div>

                }
            </div>
        </div>
    );
}

export default PortfolioForm;