using Microsoft.Owin;
using Owin;

[assembly: OwinStartupAttribute(typeof(WebAppEx.Startup))]
namespace WebAppEx
{
    public partial class Startup {
        public void Configuration(IAppBuilder app) {
            ConfigureAuth(app);
        }
    }
}
