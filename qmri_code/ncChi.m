function varargout = ncChi(varargin)
[varargout{1:nargout}] = spm_subfun(localfunctions,varargin{:});

function lp = lnpdf(x,nu,mu,sig2)
if numel(mu)==1 && mu==0
    % Chi
    lp   = ((1-nu/2)*log(2) - 0.5*nu.*log(sig2+realmin) - gammaln(nu/2)) + (nu-1).*log(x+realmin) - x.^2./(2*sig2+realmin);
else
    % Non-central Chi
    t    = (mu.*x)./(sig2+realmin);
    lp   = ((1 - nu/2).*log(mu+realmin) - log(sig2+realmin)) +...
           besseliln(nu/2-1, t) - (mu.^2 + x.^2 + realmin)./(2*sig2+realmin) + (nu/2).*log(x+realmin);
end


function p = pdf(x,nu,mu,sig)
p = exp(lnpdf(x,nu,mu,sig));


function lp = besseliln(nu,t)
lp  = zeros(size(t));
msk = t>1;
lp( msk) = log(besseli(nu,t( msk),1)) + t(msk);
lp(~msk) = log(besseli(nu,t(~msk)));


function g = dmu(x,nu,mu,sig2)
t  = (mu.*x)./(sig2+realmin);
r  =  besselr(nu/2-1,t);
g  =  (mu - x*r)/(sig2+realmin);

function r = besselr(nu,t)
if true
    r    = t./(nu+0.5+sqrt(t.^2+(nu+1).^2));
else
    r   = zeros(size(t));
    msk = t>1;
    r( msk) = besseli(nu+1,t( msk),1)./besseli(nu,t( msk),1);
    r(~msk) = besseli(nu+1,t(~msk),0)./besseli(nu,t(~msk),0);
end
